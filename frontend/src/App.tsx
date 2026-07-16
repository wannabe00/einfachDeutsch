import { Routes, Route, Navigate } from "react-router-dom"
import type { ReactNode } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { Layout } from "@/components/layout/Layout"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { PremiumLock } from "@/components/premium/PremiumLock"
import AuthPage from "@/pages/AuthPage"
import OAuthCallbackPage from "@/pages/OAuthCallbackPage"
import WelcomePage from "@/pages/WelcomePage"
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
import VideosPage from "@/pages/VideosPage"
import HistoryPage from "@/pages/HistoryPage"
import LandingPage from "@/pages/LandingPage"
import SettingsPage from "@/pages/SettingsPage"
import PathPage from "@/pages/PathPage"
import UnitPage from "@/pages/UnitPage"
import LessonPlayerPage from "@/pages/LessonPlayerPage"
import ExamPage from "@/pages/ExamPage"
import UiKitPage from "@/pages/UiKitPage"
import PrivacyPage from "@/pages/PrivacyPage"

function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
      Loading…
    </div>
  )
}

function RequireAuth({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) return <Loading />
  // Guests see the section blurred behind a sign-up/login overlay rather than
  // being redirected away.
  if (!user) return <LockedFeature />
  return <>{children}</>
}

/** Premium-only sections (AI, Recite — Spec v3). The backend is the real gate
    (`IsPremium` → 403); this just shows the upsell instead of a broken page. */
function RequirePremium({ children }: { children: ReactNode }) {
  const { user } = useAuth()
  if (!user?.has_premium) return <PremiumLock />
  return <>{children}</>
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

/** The app shell — signed-in users with unfinished onboarding are redirected. */
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
      {/* /register kept as an alias so old links still work. */}
      <Route path="/register" element={<Navigate to="/login" replace />} />
      {/* OAuth provider redirect lands here (public — no token yet). */}
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

      {/* The app shell is open to guests; individual routes decide whether
          they require an account (see lib/access.ts). */}
      <Route element={<AppShell />}>
        {/* Guest-OK (free to the owner, read-only or cheap, backend-throttled) */}
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/words" element={<WordBankPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/exercises" element={<ExercisesPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/chapters/:chapterId" element={<ChapterDetailPage />} />
        {/* Drills hub is public; individual drills gate themselves. */}
        <Route path="/drills" element={<DrillsPage />} />
        {/* Design v3 living style guide (Phase 23.2 reference). */}
        <Route path="/ui-kit" element={<UiKitPage />} />

        {/* Account-only (cost the owner / abusable / speech) */}
        {/* The path is inherently per-user (level + progress + energy). */}
        <Route
          path="/path"
          element={
            <RequireAuth>
              <PathPage />
            </RequireAuth>
          }
        />
        <Route
          path="/path/exam"
          element={
            <RequireAuth>
              <ExamPage />
            </RequireAuth>
          }
        />
        <Route
          path="/path/:unitId"
          element={
            <RequireAuth>
              <UnitPage />
            </RequireAuth>
          }
        />
        <Route
          path="/path/:unitId/lesson/:lessonId"
          element={
            <RequireAuth>
              <LessonPlayerPage />
            </RequireAuth>
          }
        />
        <Route
          path="/speak"
          element={
            <RequireAuth>
              <RequirePremium>
                <RecitePage />
              </RequirePremium>
            </RequireAuth>
          }
        />
        <Route
          path="/ai"
          element={
            <RequireAuth>
              <RequirePremium>
                <AIAssistantPage />
              </RequirePremium>
            </RequireAuth>
          }
        />
        <Route
          path="/videos"
          element={
            <RequireAuth>
              <VideosPage />
            </RequireAuth>
          }
        />
        <Route
          path="/history"
          element={
            <RequireAuth>
              <HistoryPage />
            </RequireAuth>
          }
        />
        <Route
          path="/settings"
          element={
            <RequireAuth>
              <SettingsPage />
            </RequireAuth>
          }
        />
      </Route>

      {/* Privacy is public (linked from the landing footer) and standalone. */}
      <Route path="/privacy" element={<PrivacyPage />} />
    </Routes>
  )
}

export default App
