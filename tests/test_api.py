from api.index import normalize_serpapi_response


def test_normalize_serpapi_response_shape():
    fake = {
        "search_parameters": {"q": "test dotaz"},
        "organic_results": [
            {
                "title": "A",
                "link": "https://a.example",
                "displayed_link": "a.example",
                "snippet": "aaa",
            },
            {
                "title": "B",
                "link": "https://b.example",
                "displayed_link": "b.example",
                "snippet": "bbb",
            },
        ],
    }

    out = normalize_serpapi_response(fake)

    assert out["query"] == "test dotaz"
    assert out["count"] == 2
    assert out["results"][0]["position"] == 1
    assert out["results"][0]["title"] == "A"
    assert out["results"][0]["link"].startswith("https://")
    assert out["results"][0]["displayLink"] == "a.example"
    assert out["results"][0]["snippet"] == "aaa"

