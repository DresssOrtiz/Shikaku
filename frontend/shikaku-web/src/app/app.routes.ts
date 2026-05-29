import { Routes } from '@angular/router';
import { Home } from './pages/home/home';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'what-is-shikaku', loadComponent: () => import('./pages/what-is-shikaku/what-is-shikaku').then(m => m.WhatIsShikaku) },
  { path: 'complexity', loadComponent: () => import('./pages/complexity/complexity').then(m => m.Complexity) },
  { path: 'algorithm', loadComponent: () => import('./pages/algorithm/algorithm').then(m => m.Algorithm) },
  { path: 'demo', loadComponent: () => import('./pages/demo/demo').then(m => m.Demo) },
  { path: 'benchmark', loadComponent: () => import('./pages/benchmark/benchmark').then(m => m.Benchmark) },
  { path: '**', redirectTo: '' }
];
