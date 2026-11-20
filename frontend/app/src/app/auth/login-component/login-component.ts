import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../shared/services/auth-service';
import { LoginSchemaIn } from '../../shared/services/auth-service.types';

@Component({
  selector: 'app-login-component',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login-component.html',
  styleUrl: './login-component.scss',
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  form = this.fb.group({
    email: ['', [Validators.required]],
    password: ['', [Validators.required]],
  });

  onClick() {
    if (this.form.valid) {
      const body: LoginSchemaIn = {
        email: this.form.value.email!,
        password: this.form.value.password!,
      };
      this.auth.login(body).subscribe({
        next: () => {
          this.router.navigate(['/profile']);
        },
      });
    }
  }
}
