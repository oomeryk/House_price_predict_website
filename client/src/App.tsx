import { useState } from "react"
import axios from "axios"
import Button from "./components/Button"
import Input from "./components/Input"
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material"
import rooms from "./data/Rooms"
import cities from "./data/Cities"
import districts from "./data/Districts"
import neighborhoods from "./data/Neighborhoods"

type RentalForm = {
  city: string,
  district: string,
  neighborhood: string,
  room: string,
  metrekare: string,
}

function App() {
  const [form, setForm] = useState<RentalForm>({
    city: "",
    district: "",
    neighborhood: "",
    room: "",
    metrekare: "",
  })
  const [response, setResponse] = useState({
    status : false,
    message : ""
  })

  const handleClick = async (dto : {city : string,district : string, neighborhood : string, room : string, metrekare: string})  => {
    try{
      const res =await axios.post("/api/rentalhouse", dto)
      setResponse({
        status : true,
        message : res.data
      })
    }catch(e){
      alert(e)
    }
  }

  const handleClear = () => {
    setResponse({
      status : false,
      message : ""
    })
    setForm({
      city: "",
      district: "",
      neighborhood: "",
      room: "",
      metrekare: "",
    })
  }
     
  return (
    <div className="flex flex-col gap-3 justify-center items-center h-screen">
        <FormControl className="w-60 h-15 bg-gray-300 rounded-md">
          <InputLabel id="city-select-label" className="text-black">City</InputLabel>
          <Select
            labelId="city-select-label"
            id="city-select"
            value={form.city}
            label="City"
            onChange={(e) => setForm({...form, city: e.target.value})}
          > 
            <MenuItem value="">
              None
            </MenuItem>
            {
              cities.map((city) => <MenuItem key={city.sehir_id} value={city.sehir_adi[0] + city.sehir_adi.substring(1).toLocaleLowerCase("tr-TR")}>{city.sehir_adi}</MenuItem>) 
            }
          </Select>
        </FormControl>
        <FormControl className="w-60 h-15 bg-gray-300 rounded-md">
          <InputLabel id="district-select-label">District</InputLabel>
          <Select
            labelId="district-select-label"
            id="district-select"
            disabled={!form.city}
            value={form.district}
            label="district"
            onChange={(e) => setForm({...form, district: e.target.value})}
          > 
            <MenuItem value="">
              None
            </MenuItem>
            {   
              districts.filter((district) => district.sehir_adi === form.city.toLocaleUpperCase("tr-TR")).map((district) => <MenuItem key={district.ilce_id} value={district.ilce_adi[0] + district.ilce_adi.substring(1).toLocaleLowerCase("tr-TR")}>{district.ilce_adi}</MenuItem>) 
            }
          </Select>
        </FormControl>
        <FormControl className="w-60 h-15 bg-gray-300 rounded-md">
          <InputLabel id="room-select-label">Neighborhood</InputLabel>
          <Select
            labelId="Neighborhood-select-label"
            id="Neighborhood-select"
            disabled={!form.district}
            value={form.neighborhood}
            label="Neighborhood"
            onChange={(e) => setForm({...form, neighborhood: e.target.value})}
          > 
            <MenuItem value="">
              None
            </MenuItem>
            {
              neighborhoods.filter((neighborhood) => neighborhood.sehir_adi == form.city.toLocaleUpperCase("tr-TR")  && neighborhood.ilce_adi === form.district.toLocaleUpperCase("tr-TR")).map((neighborhood) => <MenuItem key={neighborhood.mahalle_id} value={neighborhood.mahalle_adi[0] + neighborhood.mahalle_adi.substring(1).toLocaleLowerCase("tr-TR")}>{neighborhood.mahalle_adi}</MenuItem>) 
            }
          </Select>
        </FormControl>
        <FormControl className="w-60 h-15 bg-gray-300 rounded-md">
          <InputLabel id="room-select-label">Room</InputLabel>
          <Select
            labelId="room-select-label"
            id="room-select"
            value={form.room}
            label="Room"
            onChange={(e) => setForm({...form, room: e.target.value})}
          > 
            <MenuItem value="">
              None
            </MenuItem>
            {
              rooms.map((room) => <MenuItem key={room.room_id} value={room.room_name}>{room.room_name}</MenuItem>) 
            }
          </Select>
        </FormControl>
        <Input placeholder="Square meters" value={form.metrekare} onChange={(e) => setForm({...form, metrekare: e.target.value})}/>
        <Button text="Rental House" onClick={() => handleClick(form)} color="orange"/>
        {
          response.status && 
          <div className="flex flex-col gap-2 justify-center items-center  p-3">
            <p className="font-semibold text-[20px]">{response.message}</p>
            <Button text="Clear" onClick={handleClear}  color="green"/>
          </div>
        } 
    </div>
  )
}

export default App
