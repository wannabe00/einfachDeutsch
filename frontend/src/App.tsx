import { Routes, Route, Navigate } from "react-router-dom"
import type { ReactNode } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { Layout } from "@/components/layout/Layout"
import { LockedFeature } from "@/components/auth/LockedFeature"
import AuthPage from "@/pages/AuthPage"
import VerifyEmailPage from "@/pages/VerifyEmailPage"
import OnboardingPage from "@/pages/OnboardingPage"
import Dashboard from "@/pages/Dashboard"
import ReviewPage from "@/pages/ReviewPage"
import WordBankPage from "@/pages/WordBankPage"
import GrammarPage from "@/pages/GrammarPage"
import ExercisesPage from "@/pages/ExercisesPage"
import DrillsPage from "@/pages/DrillsPage"
import RecitePage from "@/pages/RecitePage"
import BooksPage from "@/pages/BooksPage"
import ChapterDetailPage from "@/pages/ChapterDetailPage"
import AIAssistantPage from "@/pages/AIAssistantPage"

function RequireAuth({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
        Loading…
      </div>
    )
  }
  // Guests see the section blurred behind a sign-up/login overlay rather than
  // being redirected away.
  if (!user) return <LockedFeature />
  return <>{children}</>
}

/** The app shell — but a signed-in user who hasn't chosen a level yet is sent
    to onboarding first. Guests pass through (they have no level to set). */
function AppShell() {
  const { user } = useAuth()
  if (user && !user.level_set) return <Navigate to="/onboarding" replace />
  return <Layout />
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
      {/* First-login level onboarding (only for signed-in users without a
          level set; once set, bounce to the app). */}
      <Route
        path="/onboarding"
        element={
          !user ? (
            <Navigate to="/login" replace />
          ) : user.level_set ? (
            <Navigate to="/" replace />
          ) : (
            <OnboardingPage />
          )
        }
      />

      {/* The app shell is open to guests; individual routes decide whether
          they require an account (see lib/access.ts). */}
      <Route element={<AppShell />}>
        {/* Guest-OK (free to the owner, read-only or cheap, backend-throttled) */}
        <Route path="/" element={<Dashboard />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/words" element={<WordBankPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/exercises" element={<ExercisesPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/chapters/:chapterId" element={<ChapterDetailPage />} />
        {/* Drills hub is public; individual drills gate themselves (Gender
            Triage is free, the rest are members-only — see DrillsPage). */}
        <Route path="/drills" element={<DrillsPage />} />

        {/* Account-only (cost the owner / abusable / speech) */}
        <Route
          path="/speak"
          element={
            <RequireAuth>
              <RecitePage />
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
