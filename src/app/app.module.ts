import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AgmCoreModule } from '@agm/core';

import{ MatInputModule } from '@angular/material/input';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { HeaderComponent } from './header/header.component';
import { AppRoutingModule } from './app-routing.module';
import { MapComponent } from './map/map.component';
import { HttpClientModule } from '@angular/common/http';
import { AddrInputService } from './addr-input.service';
import { AppService } from './app.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UserService } from './user.service';
import { UserBookmarksComponent } from './user-bookmarks/user-bookmarks.component';
import { CreateComponent } from './create/create.component';
import { LoginComponent } from './login/login.component';
import { RatingModule } from 'ngx-bootstrap/rating';
import { FooterComponent } from './footer/footer.component';
import { Home2Component } from './home2/home2.component';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    MapComponent,
    HomeComponent,
    UserBookmarksComponent,
    CreateComponent,
    LoginComponent,
    FooterComponent,
    Home2Component
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RatingModule.forRoot(),
    FormsModule,
    ReactiveFormsModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyD2QfpFioTBH5t8YSU_US-vDItosqF1Iv4',
      libraries: ['places', 'drawing', 'geometry']
    }),
    AppRoutingModule,
    BrowserModule,
    HttpClientModule,
    MatInputModule,
    MatAutocompleteModule,
    BrowserAnimationsModule
  ],
  providers: [AppService, AddrInputService, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
