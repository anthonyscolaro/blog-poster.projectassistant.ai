-- Drop existing policies on audit_logs if they exist
DROP POLICY IF EXISTS "Users can view their organization's audit logs" ON public.audit_logs;
DROP POLICY IF EXISTS "System can insert audit logs" ON public.audit_logs;
DROP POLICY IF EXISTS "Admins can manage audit logs" ON public.audit_logs;

-- Recreate audit_logs policies
CREATE POLICY "Users can view their organization's audit logs" ON public.audit_logs
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.profiles 
            WHERE profiles.id = auth.uid()
        )
    );

CREATE POLICY "System can insert audit logs" ON public.audit_logs
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Admins can manage audit logs" ON public.audit_logs
    FOR DELETE USING (
        organization_id IN (
            SELECT organization_id FROM public.profiles 
            WHERE profiles.id = auth.uid() 
            AND profiles.role IN ('owner', 'admin')
        )
    );