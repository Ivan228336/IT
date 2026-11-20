export type UserRegister = {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
};
export type LoginSchemaIn = {
  password: string;
  email: string;
};

export type LoginSchemaOut = {
  success: boolean;
  access: string;
  refresh: string;
  access_exp: string;
  refresh_exp: string;
};

export type EmailVerified = {
  message: string;
  success: boolean;
  access: string;
  refresh: string;
  access_exp: string;
  refresh_exp: string;
};

export type SuccessResponse = {
  success: boolean;
  message: string;
  detail: string | null;
};
