import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react"

interface PanelState {
  title: string
  initialPrompt: string
}

interface AIPanelContextValue {
  panel: PanelState | null
  openPanel: (title: string, initialPrompt: string) => void
  closePanel: () => void
}

const AIPanelContext = createContext<AIPanelContextValue | null>(null)

export function AIPanelProvider({ children }: { children: ReactNode }) {
  const [panel, setPanel] = useState<PanelState | null>(null)

  const openPanel = useCallback((title: string, initialPrompt: string) => {
    setPanel({ title, initialPrompt })
  }, [])
  const closePanel = useCallback(() => setPanel(null), [])

  return (
    <AIPanelContext.Provider value={{ panel, openPanel, closePanel }}>
      {children}
    </AIPanelContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAIPanel() {
  const ctx = useContext(AIPanelContext)
  if (!ctx) throw new Error("useAIPanel must be used within AIPanelProvider")
  return ctx
}
