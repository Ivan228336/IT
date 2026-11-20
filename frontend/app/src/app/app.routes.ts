import { Routes } from '@angular/router';
import { NotFound } from './not-found/not-found';
import { VerifyComponent } from './verify-component/verify-component';
import { ProfileComponent } from './profile-component/profile-component';

export const routes: Routes = [
  { path: '', redirectTo: '/auth/login', pathMatch: 'full' },
  { path: 'verify', component: VerifyComponent },
  { path: 'profile', component: ProfileComponent },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.routes').then((m) => m.authRoutes),
  },
  {
    path: '**',
    component: NotFound,
  },
];
