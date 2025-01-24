import { useState } from 'react'
import { InputFile } from './components/ui/upload'
import { ResultsTab } from './components/ui/result-content'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import './App.css'

function App() {
  const [essayContent, setEssayContent] = useState(null);
  const [score, setScore] = useState(null);
  const [description, setDescription] = useState(null);

  const handleSubmit = async (file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setEssayContent(data.essay_text);
        setScore(data.score); 
        setDescription(data.description);
      } else {
        console.error("Error uploading essay:", response.statusText);
      }
    } catch (error) {
      console.error('Error uploading essay:', error);
    }
  };

  return (
    <div>
      <Card className="max-w-2xl mx-auto shadow-xl">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold text-black-50">Automated Essay Scoring</CardTitle>
          <CardDescription>Silakan upload esai untuk mendapatkan skornya!</CardDescription>
        </CardHeader>
        <CardContent>
          <InputFile onSubmit={handleSubmit} />
          {score != null && (
            <div className="mt-1">
              <ResultsTab essayContent={essayContent} score={score} description={description} />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default App;