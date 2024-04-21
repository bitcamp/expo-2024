export interface AlgoResultType {
  id: number;
  team_name: string;
  table: string;
  in_person: boolean;
  link: string;
  challenges: Challenge[];
}

export interface Challenge {
  is_mlh: boolean;
  challenge_name: string;
  company: string;
  judge: string;
  start_time: string;
}

export interface ChallengeType {
  id: number;
  prize_category: string;
}
