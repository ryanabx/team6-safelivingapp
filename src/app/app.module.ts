import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AgmCoreModule } from '@agm/core';
import { AgmDrawingModule } from '@agm/drawing';

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


@NgModule({
  declarations: [
    AppComponent,
    CoordListComponent,
    PropertiesComponent,
    HeaderComponent,
    MapComponent,
    HomeComponent,
    PropertyViewerComponent,
    PropertyBrowserComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyD2QfpFioTBH5t8YSU_US-vDItosqF1Iv4',
      libraries: ['drawing']
    }),
    AppRoutingModule,
    BrowserModule,
    AgmDrawingModule
  ],
  providers: [AppService, AddrInputService],
  bootstrap: [AppComponent]
})
export class AppModule { }
