Feature: Interactions from reddit objects
  As a redditor, I want the bot to be able to identify different types of interactions so that I do not have to explicitly
  specify their presence in posts.

  Scenario: Song posts are identified
    Given There is a valid song submission
    Given The post is parsed
    Then I should have a SongInteraction
    And I should be able to see the track information

  Scenario: Other types of posts are not identified as song posts
    Given There is an invalid song submission
    Then I should see an InteractionParsingError upon parsing

  Scenario Outline: All song posts are identified
    Given There is a <valid> song submission from the feed
    Given A user tries to create a song interaction from it
    Then I should have a SongInteraction
    And I should be able to see the track information

    Examples:
      | valid |
      | 3     |
      | 9     |
      | 11    |
      | 13    |
      | 15    |
      | 16    |
      | 18    |

