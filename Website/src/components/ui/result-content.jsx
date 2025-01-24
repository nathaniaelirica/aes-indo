import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./card"
import { Label } from '@radix-ui/react-label'
import { Award, FileText } from 'lucide-react';

export function ResultsTab({ essayContent, score, description }) {
    return (
    <div className="max-w-2xl mx-auto mt-4 shadow-muted">
    <Tabs defaultValue="score" className="w-full mt-2">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="score" className="pt-1 bg-gray-100 focus:outline-none hover:outline-none rounded-md transition duration-300 ease-in-out">Skor</TabsTrigger>
        <TabsTrigger value="essay" className="pt-1 bg-gray-100 focus:outline-none hover:outline-none rounded-md transition duration-300 ease-in-out">Konten Esai</TabsTrigger>
      </TabsList>
      <TabsContent value="score">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Award className="mr-2 h-6 w-6" />
              Prediksi Skor Esai
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <span className="text-6xl font-bold">{score}</span>
              <span className="text-3xl text-muted-foreground">/6</span>
            </div>
            <div className="bg-yellow-50 border-l-4 border-yellow-500 text-black-900 p-4 rounded mt-3">
              <Label className='font-medium block text-justify mt-1'>Keterangan:</Label>
              <p className='text-justify mt-1'>{description}</p>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="essay">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="mr-2 h-6 w-6" />
              Konten Esai
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="whitespace-pre-wrap bg-muted p-4 rounded-md text-sm max-h-96 overflow-y-auto text-justify">
              {essayContent}
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
    </div>
    );
}