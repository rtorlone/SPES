import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RefertiComponent } from './referti.component';

describe('RefertiComponent', () => {
  let component: RefertiComponent;
  let fixture: ComponentFixture<RefertiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RefertiComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RefertiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
