import { Routes, Route } from "react-router-dom"

import { Layout } from "@/components/layout/Layout"
import Dashboard from "@/pages/Dashboard"
import ReviewPage from "@/pages/ReviewPage"
import WordBankPage from "@/pages/WordBankPage"
import GrammarPage from "@/pages/GrammarPage"
import ExercisesPage from "@/pages/ExercisesPage"
import DrillsPage from "@/pages/DrillsPage"
import SpeakPage from "@/pages/SpeakPage"
import BooksPage from "@/pages/BooksPage"
import ChapterDetailPage from "@/pages/ChapterDetailPage"
import AIAssistantPage from "@/pages/AIAssistantPage"

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/words" element={<WordBankPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/exercises" element={<ExercisesPage />} />
        <Route path="/drills" element={<DrillsPage />} />
        <Route path="/speak" element={<SpeakPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/chapters/:chapterId" element={<ChapterDetailPage />} />
        <Route path="/ai" element={<AIAssistantPage />} />
      </Route>
    </Routes>
  )
}

export default App
