import styleText from "data-text:./assets/style.content.css"
import type { PlasmoCSConfig, PlasmoGetStyle } from "plasmo"

import { ChatRoot } from "~components/chats"
import { SocketProvider } from "~providers"

function HevyAssistantRoot() {
  return (
    <SocketProvider>
      <div id="hevy-assistant-interface-root">
        <ChatRoot />
      </div>
    </SocketProvider>
  )
}

export const getStyle: PlasmoGetStyle = () => {
  const style = document.createElement("style")
  style.textContent = styleText
  return style
}

export const config: PlasmoCSConfig = {
  matches: ["https://hevy.com/*"],
  all_frames: true
}

export default HevyAssistantRoot
