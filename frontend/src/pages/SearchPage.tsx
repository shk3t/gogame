import {useActions, useAppSelector} from "../redux/hooks"
import {defaultGameSettings} from "../types/game"
import ScaryButton from "../components/buttons/ScaryButton"
import PlayerList from "../components/lists/PlayerList"
import {useEffect} from "react"
import GameService from "../services/GameService"
import {ContainerMargins} from "../types/component"
import MainContainer from "../components/containers/MainContainer"
import CenteringContainer from "../components/containers/CenteringContainer"

export default function SearchPage() {
  const settings = useAppSelector((state) => state.gameReducer.settings)
  const connectedPlayers = useAppSelector((state) => state.playerReducer.players)
  const {endGame} = useActions()

  useEffect(() => {
    if (connectedPlayers.length > 0 && !GameService.connection) endGame()
  }, [])

  return (
    <MainContainer vertical={true} margin={ContainerMargins.EVERYTHING}>
      <h1>Search...</h1>
      <CenteringContainer vertical={true} frame={true}>
        <h3>
          {connectedPlayers.length}/
          {settings.custom ? settings.players : defaultGameSettings.players}
        </h3>
        <PlayerList players={connectedPlayers} big={true} />
      </CenteringContainer>
      <ScaryButton onClick={endGame}>Cancel</ScaryButton>
    </MainContainer>
  )
}