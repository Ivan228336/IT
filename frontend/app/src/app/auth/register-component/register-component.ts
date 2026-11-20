import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../shared/services/auth-service';
import { UserRegister } from '../../shared/services/auth-service.types';

@Component({
  selector: 'app-register-component',
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './register-component.html',
  styleUrl: './register-component.scss',
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  form = this.fb.group({
    username: ['', [Validators.required]],
    email: ['', [Validators.required]],
    password: ['', [Validators.required]],
    confirmPassword: ['', [Validators.required]],
  });

  onClick() {
    if (this.form.valid) {
      const body: UserRegister = {
        username: this.form.value.username!,
        email: this.form.value.email!,
        password: this.form.value.password!,
        confirm_password: this.form.value.confirmPassword!,
      };
      this.auth.register(body).subscribe({
        next: () => {
          this.router.navigate(['/login']);
        },
      });
    }
  }
}
