# Prompt 04: Turn SRS.md into an Executive-Grade PDF

> **When to use:** Whenever a stakeholder, client, or team member asks for system documentation.  
> **How to use:** Copy the prompt below into Claude, ChatGPT, Gemini, or Claude Code, and paste your `brain/documentation/SRS.md` content directly beneath it.  
> **Output:** A single, self-contained, publication-ready HTML file with embedded executive print CSS. You simply open it in your browser, press `Ctrl+P` (or `Cmd+P`), and click **"Save as PDF"**.

---

```markdown
You are an expert technical documentation designer and typographer. I will provide you with a markdown System Requirements Specification (SRS) file. 

Your task is to convert this markdown into a single, self-contained, publication-grade HTML document styled specifically for printing to PDF via the browser ("Save as PDF").

### Visual & Typographic Requirements:
1. **Executive Cover Page:**
   - Modern, professional cover page that takes up exactly the first page (`page-break-after: always`).
   - Clean document title, subtitle, version tag (e.g., `v1.0.0`), status pill (e.g., `ACTIVE`), author/team, date, and repository link.
   - Discreet confidentiality note at the bottom: "Confidential & Proprietary — For Internal/Authorized Use Only".

2. **Table of Contents:**
   - Clean, numbered Table of Contents following the cover page.

3. **Typography & Styling:**
   - Clean font stack: `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;`.
   - Balanced line height (1.6) and high-contrast dark text (`#111827`) on clean white background.
   - Code blocks and tables in modern monospace (`ui-monospace, "SF Mono", Menlo, Consolas`).
   - Clean section headers with subtle bottom border lines.

4. **Tables & Matrices:**
   - Shaded table headers (`background-color: #f3f4f6; color: #111827; font-weight: 600;`).
   - Subtle borders (`#e5e7eb`), alternating zebra rows (`#fafafa`), and comfortable cell padding (8px 12px).
   - `page-break-inside: avoid;` on all tables so rows never get split awkwardly across page breaks.

5. **Diagrams (Mermaid):**
   - Include the Mermaid JS CDN script (`<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script><script>mermaid.initialize({startOnLoad:true, theme:'neutral'});</script>`) so all Mermaid diagrams render as crisp vector graphics.

6. **Print & Pagination Rules (`@media print`):**
   - `@page { size: A4; margin: 20mm 15mm 20mm 15mm; }`
   - Every major `h2` section starts on a fresh page (`page-break-before: always;`).
   - Subheadings `h3` and `h4` have `page-break-after: avoid;` so headings are never orphaned at the bottom of a page.
   - Footers displaying document title on the left and dynamic page numbers on the right.

---

### Input Markdown:
[PASTE YOUR brain/documentation/SRS.md CONTENT HERE]
```
