import { useState } from 'react';
import { Button } from "./button";
import { Input } from "./input";
import { Label } from "./label";
import { Upload } from "lucide-react";

export function InputFile({ onSubmit }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onSubmit(file);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="essay-file" className="text-base font-medium block text-justify">
          Upload Esai
        </Label>
        <div className="flex items-center space-x-2">
          <Input
            id="essay-file"
            type="file"
            accept=".txt, .pdf, .docx"
            onChange={handleFileChange}
            required
            className="flex-grow"
          />
          <div className="shrink-0">
            <Button type="submit" disabled={!file} className="w-full">
              <Upload className="mr-2 h-4 w-4" />
              Submit
            </Button>
          </div>
        </div>
      </div>
      {file && (
        <p className="text-sm text-muted-foreground text-justify">
          File: {file.name}
        </p>
      )}
    </form>
  );
}
