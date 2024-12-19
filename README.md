Scrape Wikipedia outline and category page in JSON

Category source page: https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories  
Outline source page: https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines  

#### Usage
check `result.json` or run `run.py` to fetch latest source and filter

#### Example

##### category
```
{
    "subject": "History and events",
    "level": 1,
    "children": [
      "By period",
      "By topic(Science·Religion)",
      "Historiography",
      "Timelines",
      {
        "subject": "History by location",
        "level": 2,
        "children": [],
        "subcategory": [
          [
            {
              "subject": "By continent",
              "level": 3,
              "children": [
                "Africa",
                "Asia",
                "Europe",
                "America"
              ],
              "subcategory": []
            },
            {
              "subject": "By region",
              "level": 3,
              "children": [
                "North America",
                "South America",
                "Central Europe",
                "West Asia",
                "Oceania"
              ],
              "subcategory": []
            },
            {
              "subject": "By country",
              "level": 3,
              "children": [
                "By city",
                "Empires"
              ],
              "subcategory": []
            }
          ],
          [
            {
              "subject": "By region",
              "level": 3,
              "children": [
                "North America",
                "South America",
                "Central Europe",
                "West Asia",
                "Oceania"
              ],
              "subcategory": []
            },
            {
              "subject": "By country",
              "level": 3,
              "children": [
                "By city",
                "Empires"
              ],
              "subcategory": []
            }
          ],
          [
            {
              "subject": "By country",
              "level": 3,
              "children": [
                "By city",
                "Empires"
              ],
              "subcategory": []
            }
          ]
        ]
      }
    ]
  }
```

--- 

##### outline
```
{
    "subject": "Culture and the arts",
    "level": 1,
    "children": {
        "subject": "Culture",
        "level": 2,
        "children": [
            {
                "subject": "The arts",
                "level": 3,
                "children": [
                    {
                        "subject": "Literature",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Fiction",
                                "level": 5
                            },
                            {
                                "subject": "Poetry",
                                "level": 5
                            },
                            {
                                "subject": "Critical theory",
                                "level": 5
                            }
                        ]
                    },
                    {
                        "subject": "Visual arts",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Architecture",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Classical architecture",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Crafts",
                                "level": 5
                            },
                            {
                                "subject": "Drawing",
                                "level": 5
                            },
                            {
                                "subject": "Design",
                                "level": 5
                            },
                            {
                                "subject": "Film",
                                "level": 5
                            },
                            {
                                "subject": "Painting",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "History of painting",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Photography",
                                "level": 5
                            },
                            {
                                "subject": "Sculpture",
                                "level": 5
                            }
                        ]
                    },
                    {
                        "subject": "Performing arts",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Acting",
                                "level": 5
                            },
                            {
                                "subject": "Dance",
                                "level": 5
                            },
                            {
                                "subject": "Film",
                                "level": 5
                            },
                            {
                                "subject": "Theatre",
                                "level": 5
                            },
                            {
                                "subject": "Music",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Classical music",
                                        "level": 6,
                                        "children": [
                                            {
                                                "subject": "Classical music",
                                                "level": 7
                                            },
                                            {
                                                "subject": "Jazz",
                                                "level": 7
                                            },
                                            {
                                                "subject": "Opera",
                                                "level": 7
                                            }
                                        ]
                                    },
                                    {
                                        "subject": "Guitars",
                                        "level": 6,
                                        "children": [
                                            {
                                                "subject": "Guitars",
                                                "level": 7
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "subject": "Stagecraft",
                                "level": 5
                            }
                        ]
                    }
                ]
            },
            {
                "subject": "Gastronomy",
                "level": 3,
                "children": [
                    {
                        "subject": "Food preparation",
                        "level": 4
                    },
                    {
                        "subject": "Cuisines",
                        "level": 4
                    },
                    {
                        "subject": "Meals",
                        "level": 4
                    },
                    {
                        "subject": "Food, human food and drink",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Chocolate",
                                "level": 5
                            },
                            {
                                "subject": "Herbs",
                                "level": 5
                            },
                            {
                                "subject": "Spices",
                                "level": 5
                            },
                            {
                                "subject": "Strawberries",
                                "level": 5
                            },
                            {
                                "subject": "Wine",
                                "level": 5
                            },
                            {
                                "subject": "Whisky",
                                "level": 5
                            }
                        ]
                    }
                ]
            },
            {
                "subject": "Recreation and Entertainment",
                "level": 3,
                "children": [
                    {
                        "subject": "Festivals",
                        "level": 4
                    },
                    {
                        "subject": "Tourism",
                        "level": 4
                    },
                    {
                        "subject": "Fiction",
                        "level": 4,
                        "children": [
                            {
                                "subject": "James Bond",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "James Bond",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Fantasy",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "A Song of Ice and Fire franchise",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Harry Potter",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Marvel Cinematic Universe",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Middle-earth",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Narnia",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Science fiction",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Star Trek",
                                        "level": 6
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "subject": "Games",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Chess",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Chess",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Poker",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Poker",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Video games",
                                "level": 5
                            }
                        ]
                    },
                    {
                        "subject": "Sports",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Ball games",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Association football",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Baseball",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Basketball",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Golf",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Tennis",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Combat sports",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Fencing",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Martial arts",
                                        "level": 6
                                    }
                                ]
                            },
                            {
                                "subject": "Auto racing",
                                "level": 5,
                                "children": [
                                    {
                                        "subject": "Auto racing",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Canoeing and kayaking",
                                        "level": 6,
                                        "children": [
                                            {
                                                "subject": "Canoeing and kayaking",
                                                "level": 7
                                            },
                                            {
                                                "subject": "Sailing",
                                                "level": 7
                                            }
                                        ]
                                    },
                                    {
                                        "subject": "Cycling",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Motorcycling",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Running",
                                        "level": 6
                                    },
                                    {
                                        "subject": "Skiing",
                                        "level": 6
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "subject": "Area studies",
                "level": 3,
                "children": [
                    {
                        "subject": "Area studies",
                        "level": 4,
                        "children": [
                            {
                                "subject": "Sinology",
                                "level": 5
                            }
                        ]
                    },
                    {
                        "subject": "Classical studies",
                        "level": 4
                    }
                ]
            }
        ]
    }
}
```
