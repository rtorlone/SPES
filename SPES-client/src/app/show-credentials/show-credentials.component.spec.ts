import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowCredentialsComponent } from './show-credentials.component';

describe('ShowCredentialsComponent', () => {
  let component: ShowCredentialsComponent;
  let fixture: ComponentFixture<ShowCredentialsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowCredentialsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowCredentialsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
