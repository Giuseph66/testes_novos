export interface EmailAccount {
  id: string;
  email: string;
  password: string;
  uses: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface User {
  id: string;
  username: string;
  password: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
} 