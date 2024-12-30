import { useEffect, useState, useRef } from 'react'
import { useAuth } from './AuthContext'
import '../App.css'

const Navbar = ({ isAuthenticated }) => {
  return (
    <nav className="navs">
      { isAuthenticated ? (
        <h2>Welcome</h2>
        )
        : (
          <p>Log in to post reviews</p>
        )
      }
    </nav>
  )
}

function Main() {
  // handleReviewGame modifies the raw text of the game input field
  // and handleGameSelected is an event handler that fills the input field with the selected game in the dropdown

  const [reviewTitle, setReviewTitle] = useState('')
  const [reviewText, setReviewText] = useState('')
  const [reviewRating, setReviewRating] = useState('')
  const [reviews, setReviews] = useState([]) // Ensure reviews is initialized as an array
  const [games, setGames] = useState([])
  const [reviewGame, setReviewGame] = useState('')
  const [dropdownVisible, setDropdownVisible] = useState(false)
  const [reviewSent, setReviewSent] = useState(false)
  const [error, setError] = useState('')
  const { isAuthenticated } = useAuth()
  const debounceTimeout = useRef(null)

  const sendReview = async (data) => {
    try {
      const response = await fetch('http://localhost:8000/reviews', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('An error has occurred while sending the review')
      }
    } catch (error) {
      setError('An error has occurred while sending the review');
      console.error('send review error caught');
    }
  }

  const handleReviewGame = (event) => {
    setReviewGame(event.target.value)
    setDropdownVisible(true)
  }

  const handleGameSelected = (game) => {
    setReviewGame(game)
    setDropdownVisible(false)
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    if (reviewTitle && reviewText && reviewRating && reviewGame) {
      const data = {
        title: reviewTitle,
        text: reviewText,
        rating: reviewRating.toString(),
        game: reviewGame,
      }
      sendReview(data)
      setReviewSent(!reviewSent)     
      setReviewTitle('')
      setReviewText('')
      setReviewRating('')
      setReviewGame('')
    } else {
      setError('Please fill all the fields')
    }
  }


  useEffect(() => {
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current)
    }

    // I learned how to debounce this fetch request for not having request overriding with Claude's advice
    debounceTimeout.current = setTimeout(() => {
      const fetchGames = async () => {
        try {
          const response = await fetch('http://localhost:8000/games', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: reviewGame }),
          });
          if (!response.ok) {
            throw new Error('An error has occurred while fetching games')
          }

          const data = await response.json();
          console.log(data);
          setGames(data);
        } catch (error) {
          setError('An error has occurred while fetching games');
          console.log("fetch games error caught");
        }
      }
      fetchGames()
    }, 300)

    return () => {
      if (debounceTimeout.current) {
        clearTimeout(debounceTimeout.current)
      }
    }
  }, [reviewGame])

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('http://localhost:8000/reviews', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
          throw new Error('An error has occurred while fetching reviews')
        }

        const data = await response.json();
        console.log(data);
        setReviews(data);
      } catch (error) {
        setError('An error has occurred while fetching reviews')
        console.error('fetch reviews error caught');
      }
    }
    fetchReviews()
  }, [reviewSent])

  return (
    <>
        <Navbar isAuthenticated={isAuthenticated} />
        <main>
          {isAuthenticated ? (
            <div className="review-write">
              
              <form className="form-input" onSubmit={handleSubmit}>
                <h2>📜 Write your review</h2>
                <input className="inputs" value={reviewTitle} onChange={(e) => setReviewTitle(e.target.value)} placeholder="Title" />
                <input className="inputs" value={reviewText} onChange={(e) => setReviewText(e.target.value)} placeholder="Review" />
                <input type="number" className="inputs" value={reviewRating} onChange={(e) => setReviewRating(e.target.value)} min="0" max="10" placeholder="Rating" />
                <input className="inputs" value={reviewGame} onChange={handleReviewGame} placeholder="Game" />
                {dropdownVisible && games.length > 0 && (
                  <ul>
                    {games.map(game => (
                      <li key={game.id} onClick={() => handleGameSelected(game.name)}>
                        {game.name}
                      </li>
                    ))}
                  </ul>
                )}
                <button type="submit">Submit</button>
                {error && <p>{error}</p>}
              </form>
            </div>
          ) : (
            <p>Please log in to write a review</p>
          )}
          <div className="review-show">
            { reviews ?
                reviews.map(review => (
                  <div className="review" key={review.id}>
                    <h2>{review.title}</h2>
                    <p>{review.text}</p>
                    <p>{review.rating}</p>
                    <p>{review.game}</p>
                  </div>
                ))
              : <p>No reviews</p>
            }
          </div>
        </main>
    </>
  )
}

export default Main