import TextField from '@mui/material/TextField';

type Props = {
    placeholder: string;
    value : string;
    onChange : (e: React.ChangeEvent<HTMLInputElement>) => void;
}

function Input(props : Props){
    const {placeholder,value,onChange} = props;
    return <TextField type="text" variant="outlined" label={placeholder} value={value} onChange={onChange}  className="bg-gray-300 outline-none rounded-md p-2 text-[16px] h-15 w-60 "/>
}

export default Input;