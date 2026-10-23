import { inject, Injectable } from '@angular/core';
import { UserRegister } from './auth-service.types';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'https://localhost:8080/api';

  register(body: UserRegister) {
    console.log(body);
    this.http
      .post<UserRegister>(this.apiUrl + '/auth/register', body)
      .subscribe({
        next: (user) => console.log('Создан пользователь:', user),
        error: (error) => console.error('Ошибка:', error),
      });
  }
}
