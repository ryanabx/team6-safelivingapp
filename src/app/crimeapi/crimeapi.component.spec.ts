import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CrimeapiComponent } from './crimeapi.component';

describe('CrimeapiComponent', () => {
  let component: CrimeapiComponent;
  let fixture: ComponentFixture<CrimeapiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CrimeapiComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CrimeapiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
