-- Anonymous capability-based drafts: no names, IDs, documents or query text.
CREATE TABLE public.service_sources (
 id text PRIMARY KEY,
 title text NOT NULL,
 url text NOT NULL CHECK (url LIKE 'https://%'),
 reviewed_on date NOT NULL,
 version text NOT NULL
);
CREATE TABLE public.preparation_drafts (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 token_hash text NOT NULL UNIQUE,
 source_id text NOT NULL REFERENCES public.service_sources(id),
 language text NOT NULL CHECK (language IN ('en','te')),
 channel text NOT NULL CHECK (channel IN ('citizen','centre')),
 employment text NOT NULL CHECK (employment IN ('salaried','self','other')),
 identity_ready boolean NOT NULL DEFAULT false,
 income_ready boolean NOT NULL DEFAULT false,
 photo_ready boolean NOT NULL DEFAULT false,
 form_ready boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.preparation_feedback (
 draft_id uuid PRIMARY KEY REFERENCES public.preparation_drafts(id) ON DELETE CASCADE,
 helpful boolean NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.service_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.preparation_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.preparation_feedback ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.service_sources, public.preparation_drafts, public.preparation_feedback FROM anon, authenticated;
GRANT SELECT ON public.service_sources TO anon, authenticated;
CREATE POLICY sources_public_read ON public.service_sources FOR SELECT TO anon, authenticated USING (true);
INSERT INTO public.service_sources VALUES
 ('income-form', 'Telangana income certificate application form', 'https://www.telangana.gov.in/wp-content/uploads/2023/03/IncomeGeneralApplicationForm.pdf', '2026-10-23', 'published-form-2023-03'),
 ('meeseva-faq', 'Telangana mobile governance FAQ', 'https://mgov.telangana.gov.in/faqnew.html', '2026-10-23', 'published-faq-reviewed-2026-10-23'),
 ('state-services', 'Telangana public utility forms', 'https://www.telangana.gov.in/services/public-utility-forms/', '2026-10-23', 'published-index-reviewed-2026-10-23');

-- Only this bounded RPC can touch private drafts. A 256-bit bearer capability
-- is hashed before storage; no unauthenticated table reads are granted.
CREATE FUNCTION public.sevapath_draft(p_action text, p_token text, p_data jsonb DEFAULT '{}'::jsonb)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER
SET search_path = pg_catalog, public, pg_temp AS $$
DECLARE
 h text;
 d public.preparation_drafts;
BEGIN
 IF p_token IS NULL OR p_token !~ '^[a-f0-9]{64}$' THEN
   RAISE EXCEPTION 'Invalid draft key' USING ERRCODE = '22023';
 END IF;
 h := encode(sha256(convert_to(p_token, 'UTF8')), 'hex');
 IF p_action = 'save' THEN
   IF jsonb_typeof(p_data) IS DISTINCT FROM 'object' OR octet_length(p_data::text) > 1024 THEN
     RAISE EXCEPTION 'Invalid preparation data' USING ERRCODE = '22023';
   END IF;
   IF EXISTS (SELECT 1 FROM jsonb_object_keys(p_data) k WHERE k NOT IN
     ('language','channel','employment','identity_ready','income_ready','photo_ready','form_ready')) THEN
     RAISE EXCEPTION 'Unknown field: personal data is not accepted' USING ERRCODE = '22023';
   END IF;
   INSERT INTO public.preparation_drafts(token_hash,source_id,language,channel,employment,identity_ready,income_ready,photo_ready,form_ready)
   VALUES (h,'income-form',coalesce(p_data->>'language','en'),coalesce(p_data->>'channel','citizen'),coalesce(p_data->>'employment','other'),
     coalesce((p_data->>'identity_ready')::boolean,false),coalesce((p_data->>'income_ready')::boolean,false),
     coalesce((p_data->>'photo_ready')::boolean,false),coalesce((p_data->>'form_ready')::boolean,false))
   ON CONFLICT (token_hash) DO UPDATE SET
     language=EXCLUDED.language,channel=EXCLUDED.channel,employment=EXCLUDED.employment,
     identity_ready=EXCLUDED.identity_ready,income_ready=EXCLUDED.income_ready,
     photo_ready=EXCLUDED.photo_ready,form_ready=EXCLUDED.form_ready,updated_at=now()
   RETURNING * INTO d;
 ELSIF p_action = 'load' THEN
   SELECT * INTO d FROM public.preparation_drafts WHERE token_hash=h;
   IF d.id IS NULL THEN RETURN jsonb_build_object('draft',NULL); END IF;
 ELSIF p_action = 'delete' THEN
   DELETE FROM public.preparation_drafts WHERE token_hash=h;
   RETURN jsonb_build_object('deleted',true);
 ELSIF p_action = 'feedback' THEN
   SELECT * INTO d FROM public.preparation_drafts WHERE token_hash=h;
   IF d.id IS NULL THEN RAISE EXCEPTION 'Save your preparation first' USING ERRCODE='22023'; END IF;
   IF jsonb_typeof(p_data->'helpful') IS DISTINCT FROM 'boolean' THEN
     RAISE EXCEPTION 'Feedback must be a boolean' USING ERRCODE='22023';
   END IF;
   INSERT INTO public.preparation_feedback(draft_id,helpful) VALUES(d.id,(p_data->>'helpful')::boolean)
   ON CONFLICT(draft_id) DO UPDATE SET helpful=EXCLUDED.helpful;
   RETURN jsonb_build_object('recorded',true);
 ELSE
   RAISE EXCEPTION 'Unknown action' USING ERRCODE='22023';
 END IF;
 RETURN jsonb_build_object('draft',to_jsonb(d)-'token_hash',
   'ready',d.identity_ready AND d.income_ready AND d.photo_ready AND (d.channel='citizen' OR d.form_ready));
END;
$$;
REVOKE ALL ON FUNCTION public.sevapath_draft(text,text,jsonb) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.sevapath_draft(text,text,jsonb) TO anon, authenticated;
