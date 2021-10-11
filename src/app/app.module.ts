import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { AppService } from './app.service';

import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { CoordListComponent } from './coord-list/coord-list.component';
import { AddrInputService } from './addr-input.service';

// array for easy management of routes
// runGuardsAndResolvers used in reloading components
const routes: Routes = [
  {path: 'coord-list', component: CoordListComponent,
    
   runGuardsAndResolvers: 'always'}
]

@NgModule({
  declarations: [
    AppComponent,
    CoordListComponent
  ],
  imports: [
    BrowserModule,
    //onSameUrlNavigation used for reloading routes when already on them
    RouterModule.forRoot(routes, {onSameUrlNavigation: 'reload'}), 
    HttpClientModule
  ],
  providers: [AppService, AddrInputService],
  bootstrap: [AppComponent]
})
export class AppModule { }
