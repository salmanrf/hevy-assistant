export type HevyUser = {
  hevy_user_id: string
  username: string
  email: string
  sex: string
  birthday: string
}

export type User = HevyUser & {
  _id: string
  created_at: Date | string
  updated_at: Date | string
}
