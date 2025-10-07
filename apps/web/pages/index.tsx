
import { useState } from "react";

export default function Home() {
  const [q, setQ] = useState("");
  const [resp, setResp] = useState<any>(null);
  const ask = async () => {
    const r = await fetch("http://localhost:8080/v1/answer", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ question: q, k: 10 })
    });
    setResp(await r.json());
  };
  return (
    <div style={{padding: 24, maxWidth: 900, margin: "0 auto", fontFamily: "ui-sans-serif"}}>
      <h1>CodeAtlas RAG</h1>
      <p>Ask questions about your repo and get grounded answers with citations.</p>
      <div style={{display:"flex", gap: 8}}>
        <input style={{flex:1, padding: 8, border: "1px solid #ccc"}} value={q} onChange={e=>setQ(e.target.value)} placeholder="e.g., Where do we configure DB pool?" />
        <button onClick={ask} style={{padding: "8px 12px"}}>Ask</button>
      </div>
      {resp && (
        <div style={{marginTop:20}}>
          <h3>Answer</h3>
          <pre style={{whiteSpace:"pre-wrap"}}>{resp.answer}</pre>
          <h4>Citations</h4>
          <ul>{resp.citations.map((c: string, i: number)=><li key={i}>{c}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
