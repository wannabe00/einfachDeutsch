import { Routes, Route, Navigate, useLocation } from "react-router-dom"
import type { ReactNode } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { Layout } from "@/components/layout/Layout"
import AuthPage from "@/pages/AuthPage"
import VerifyEmailPage from "@/pages/VerifyEmailPage"
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

function RequireAuth({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()
  const location = useLocation()
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
        Loading…
      </div>
    )
  }
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />
  return <>{children}</>
}

function App() {
  const { user } = useAuth()

  return (
    <Routes>
      {/* Public auth routes (redirect to app if already signed in) */}
      <Route
        path="/login"
        element={user ? <Navigate to="/" replace /> : <AuthPage mode="login" />}
      />
      <Route
        path="/register"
        element={user ? <Navigate to="/" replace /> : <AuthPage mode="register" />}
      />
      <Route path="/verify-email/:key" element={<VerifyEmailPage />} />

      {/* The app shell is open to guests; individual routes decide whether
          they require an account (see lib/access.ts). */}
      <Route element={<Layout />}>
        {/* Guest-OK (free to the owner, read-only or cheap, backend-throttled) */}
        <Route path="/" element={<Dashboard />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/words" element={<WordBankPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/exercises" element={<ExercisesPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/chapters/:chapterId" element={<ChapterDetailPage />} />

        {/* Account-only (cost the owner / abusable / speech) */}
        <Route
          path="/drills"
          element={
            <RequireAuth>
              <DrillsPage />
            </RequireAuth>
          }
        />
        <Route
          path="/speak"
          element={
            <RequireAuth>
              <SpeakPage />
            </RequireAuth>
          }
        />
        <Route
          path="/ai"
          element={
            <RequireAuth>
              <AIAssistantPage />
            </RequireAuth>
          }
        />
      </Route>
    </Routes>
  )
}

export default App
