export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { prompt, image_base64 } = req.body;

  if (!prompt || !image_base64) {
    return res.status(400).json({ error: "Missing prompt or image_base64" });
  }

  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [
        {
          role: "user",
          parts: [
            { text: prompt },
            {
              inline_data: {
                mime_type: "image/jpeg",
                data: image_base64
              }
            }
          ]
        }
      ]
    })
  });

  const data = await response.json();

  if (!response.ok) {
    return res.status(response.status).json({ error: "Gemini API error", details: data });
  }

  const result = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? "No response";
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.json({ response: result });
}
