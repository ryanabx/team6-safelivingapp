import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserBookmarksComponent } from './user-bookmarks.component';

describe('UserBookmarksComponent', () => {
  let component: UserBookmarksComponent;
  let fixture: ComponentFixture<UserBookmarksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserBookmarksComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserBookmarksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
