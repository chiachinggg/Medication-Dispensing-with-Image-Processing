export async function testGet(){
  const url = `${import.meta.env.VITE_APP_ENDPOINT}/test`
  try {
    const response = await fetch(url, {
      method: 'GET',
    })
    const data = await response.json()
    console.log(data)
  } catch (error) {
    console.error('Error:', error)
  }
};

export async function testPost(){
    const url = `${import.meta.env.VITE_APP_ENDPOINT}/test_post`
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({id: 1, name: 'John Doe'})
        })
        const data = await response.json()
        console.log(data)
    } catch (error) {
        console.error('Error:', error)
    }
};

export async function storeImageToFolder(base64, filename) {
    const url = `${import.meta.env.VITE_APP_ENDPOINT}/store_image`
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({image: base64, filename})
        })
        const data = await response.json()
        return data
    } catch (error) {
        console.error('Error:', error)
    }
};