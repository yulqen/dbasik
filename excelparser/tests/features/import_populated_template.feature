
# Created by lemon at 19/09/18
Feature: A user can import a populated template
  So that I can get the data from a populated template,
  As a user (authentication not involved in this test)
  I want to be able to import a populated template for a Project and associate
  the resulting data with a Financial Quarter.

  Scenario: Import data from a populated template
    Given a Financial Quarter and a Project
      When the user submits a populated template containing valid data
      Then the data from the template is imported into the system
