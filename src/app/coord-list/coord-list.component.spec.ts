import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CoordListComponent } from './coord-list.component';

describe('CoordListComponent', () => {
  let component: CoordListComponent;
  let fixture: ComponentFixture<CoordListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CoordListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CoordListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
