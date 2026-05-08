import { useState, useCallback } from "react";

export default function useFetch() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const request = useCallback(async (input, init = {}) => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(input, init);
            if (!res.ok) {
                let body = null;
                try { body = await res.json(); } catch (e) { /* ignore */ }
                const msg = (body && (body.detail || body.error || body.signal || body.message)) || res.statusText || 'Request failed';
                const err = new Error(msg);
                err.status = res.status;
                throw err;
            }

            const contentType = res.headers.get("content-type") || "";
            if (contentType.includes("application/json")) {
                return await res.json();
            }

            // return response for binary downloads or other content types
            return res;
        } catch (err) {
            setError(err);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return { loading, error, request };
}
