import {useActions, useAppSelector} from "../../hooks/redux"
import styles from "../../styles/base.module.css"

export default function PlayerForm() {
  const nickname = useAppSelector((state) => state.playerReducer.currentPlayer.nickname)
  const {updateNickname} = useActions()

  return (
    <input
      className={styles.niceInput}
      value={nickname}
      onChange={(e) => updateNickname(e.target.value)}
    ></input>
  )
}