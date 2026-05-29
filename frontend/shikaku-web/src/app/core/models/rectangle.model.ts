import { Clue } from './board.model';
export type ClueTuple = [number, number, number];

export interface Rectangle {
  top: number;
  left: number;
  bottom: number;
  right: number;
  clue?: ClueTuple | Clue;
}
