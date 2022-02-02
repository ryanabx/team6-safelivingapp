import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { PropertyViewerComponent } from './properties/property-viewer/property-viewer.component';
import { HomeComponent } from './home/home.component';
import { PropertyBrowserComponent } from './properties/property-browser/property-browser.component';
import { PropertiesComponent } from './properties/properties.component';
import { HeaderComponent } from './header/header.component';
import { AppRoutingModule } from './app-routing.module';
import { MapComponent } from './map/map.component';
import { HttpClientModule } from '@angular/common/http';
import { CoordListComponent } from './coord-list/coord-list.component';
import { AddrInputService } from './addr-input.service';
import { AppService } from './app.service';
import { FormsModule } from '@angular/forms';
import { UserService } from './user.service';
import { CrimeapiComponent } from './crimeapi/crimeapi.component';
import { UserBookmarksComponent } from './user-bookmarks/user-bookmarks.component';
import { CreateComponent } from './create/create.component';
import { LoginComponent } from './login/login.component';
import {RatingModule} from 'ngx-bootstrap/rating'

@NgModule({
  declarations: [
    AppComponent,
    CoordListComponent,
    PropertiesComponent,
    HeaderComponent,
    MapComponent,
    HomeComponent,
    PropertyViewerComponent,
    PropertyBrowserComponent,
    CrimeapiComponent,
    UserBookmarksComponent,
    CreateComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RatingModule.forRoot(),
    FormsModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyD2QfpFioTBH5t8YSU_US-vDItosqF1Iv4',
      libraries: ['places', 'drawing', 'geometry']
    }),
    AppRoutingModule,
    BrowserModule,
    HttpClientModule
  ],
  providers: [AppService, AddrInputService, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
