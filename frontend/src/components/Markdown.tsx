import DOMPurify from "dompurify";
import { marked } from "marked";
import { useMemo } from "react";

marked.setOptions({ gfm: true, breaks: false });

/** Renders agent-written markdown. LLM output is untrusted, so it is sanitised before insertion. */
export function Markdown({ text, streaming = false }: { text: string; streaming?: boolean }) {
  const html = useMemo(() => {
    const raw = marked.parse(text || "", { async: false }) as string;
    const clean = DOMPurify.sanitize(raw, { USE_PROFILES: { html: true } });
    return clean.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, "</table></div>");
  }, [text]);
  return (
    <div className="prose">
      <div dangerouslySetInnerHTML={{ __html: html }} />
      {streaming && <span className="caret live" />}
    </div>
  );
}
