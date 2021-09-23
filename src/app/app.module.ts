import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { PropertyViewerComponent } from './properties/property-viewer/property-viewer.component';
import { HomeComponent } from './home/home.component';
import { PropertyBrowserComponent } from './properties/property-browser/property-browser.component';
import { PropertiesComponent } from './properties/properties.component';
import { HeaderComponent } from './header/header.component';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    PropertyViewerComponent,
    HomeComponent,
    PropertyBrowserComponent,
    PropertiesComponent,
    HeaderComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
