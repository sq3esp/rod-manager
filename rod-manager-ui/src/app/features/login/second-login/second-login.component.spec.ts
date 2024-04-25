import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SecondLoginComponent } from './second-login.component';

describe('SecondLoginComponent', () => {
  let component: SecondLoginComponent;
  let fixture: ComponentFixture<SecondLoginComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SecondLoginComponent]
    });
    fixture = TestBed.createComponent(SecondLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
