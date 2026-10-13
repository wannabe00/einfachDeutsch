import { Navigate, Outlet, Route, Routes } from "react-router-dom"

import { useAuth } from "@/contexts/AuthContext"
import { Layout } from "@/components/layout/Layout"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { PremiumLock } from "@/components/premium/PremiumLock"
import AuthPage from "@/pages/AuthPage"
import OAuthCallbackPage from "@/pages/OAuthCallbackPage"
import WelcomePage from "@/pages/WelcomePage"
import OnboardingPage from "@/pages/OnboardingPage"
import Dashboard from "@/pages/dashboard/DashboardPage"
import ReviewPage from "@/pages/ReviewPage"
import WordBankPage from "@/pages/WordBankPage"
import GrammarPage from "@/pages/GrammarPage"
import ExercisesPage from "@/pages/ExercisesPage"
import DrillsPage from "@/pages/DrillsPage"
import RecitePage from "@/pages/RecitePage"
import BooksPage from "@/pages/BooksPage"
import ChapterDetailPage from "@/pages/ChapterDetailPage"
import AIAssistantPage from "@/pages/AIAssistantPage"
import VideosPage from "@/pages/VideosPage"
import HistoryPage from "@/pages/HistoryPage"
import LandingPage from "@/pages/LandingPage"
import SettingsPage from "@/pages/SettingsPage"
import PathPage from "@/pages/path/PathPage"
import UnitPage from "@/pages/UnitPage"
import LessonPlayerPage from "@/pages/LessonPlayerPage"
import ExamPage from "@/pages/ExamPage"
import PrivacyPage from "@/pages/PrivacyPage"

function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
      Loading…
    </div>
  )
}

/** Account-only routes. Guests see the page locked behind a sign-in prompt
    instead of being redirected away. */
function RequireAuth() {
  const { user, loading } = useAuth()
  if (loading) return <Loading />
  if (!user) return <LockedFeature />
  return <Outlet />
}

/** Premium-only routes. The API enforces this too (403); here we show the
    upgrade prompt instead of a page full of failed requests. */
function RequirePremium() {
  const { user } = useAuth()
  if (!user?.has_premium) return <PremiumLock />
  return <Outlet />
}

/** A signed-in user must finish profile setup, then level onboarding, before
    reaching the app. Returns the redirect target, or null if they're ready. */
function pendingOnboardingPath(user: {
  profile_complete: boolean
  level_set: boolean
}): string | null {
  if (!user.profile_complete) return "/welcome"
  if (!user.level_set) return "/onboarding"
  return null
}

/** The app shell. Signed-in users with unfinished onboarding are redirected. */
function AppShell() {
  const { user } = useAuth()
  if (user) {
    const next = pendingOnboardingPath(user)
    if (next) return <Navigate to={next} replace />
  }
  return <Layout />
}

/** Root: marketing landing for guests, dashboard for signed-in users. */
function Home() {
  const { user, loading } = useAuth()
  if (loading) return <Loading />
  if (!user) return <LandingPage />
  const next = pendingOnboardingPath(user)
  if (next) return <Navigate to={next} replace />
  return (
    <Layout>
      <Dashboard />
    </Layout>
  )
}

function App() {
  const { user } = useAuth()

  return (
    <Routes>
      {/* Sign in (Google/GitHub or username+password). */}
      <Route
        path="/login"
        element={user ? <Navigate to="/" replace /> : <AuthPage />}
      />
      {/* Old links to /register still work. */}
      <Route path="/register" element={<Navigate to="/login" replace />} />
      {/* OAuth providers redirect here before we have a token. */}
      <Route path="/auth/callback/:provider" element={<OAuthCallbackPage />} />

      {/* Root: landing page (guests) or dashboard (signed-in). */}
      <Route path="/" element={<Home />} />

      {/* First-run profile setup (username/password/name) after social signup. */}
      <Route
        path="/welcome"
        element={
          !user ? (
            <Navigate to="/login" replace />
          ) : user.profile_complete ? (
            <Navigate to="/" replace />
          ) : (
            <WelcomePage />
          )
        }
      />
      {/* Level onboarding (after profile setup, before the app). */}
      <Route
        path="/onboarding"
        element={
          !user ? (
            <Navigate to="/login" replace />
          ) : !user.profile_complete ? (
            <Navigate to="/welcome" replace />
          ) : user.level_set ? (
            <Navigate to="/" replace />
          ) : (
            <OnboardingPage />
          )
        }
      />

      {/* The app shell is open to guests; routes below opt into auth. */}
      <Route element={<AppShell />}>
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/words" element={<WordBankPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/exercises" element={<ExercisesPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/chapters/:chapterId" element={<ChapterDetailPage />} />
        {/* The drills hub is public; individual drills gate themselves. */}
        <Route path="/drills" element={<DrillsPage />} />

        <Route element={<RequireAuth />}>
          <Route path="/path" element={<PathPage />} />
          <Route path="/path/exam" element={<ExamPage />} />
          <Route path="/path/:unitId" element={<UnitPage />} />
          <Route path="/path/:unitId/lesson/:lessonId" element={<LessonPlayerPage />} />
          <Route path="/videos" element={<VideosPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/settings" element={<SettingsPage />} />

          <Route element={<RequirePremium />}>
            <Route path="/speak" element={<RecitePage />} />
            <Route path="/ai" element={<AIAssistantPage />} />
          </Route>
        </Route>
      </Route>

      {/* Linked from the landing footer, so it lives outside the app shell. */}
      <Route path="/privacy" element={<PrivacyPage />} />
    </Routes>
  )
}

export default App
