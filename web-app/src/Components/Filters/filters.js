import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import "./style.css";

function Filters({
    autoCompleteList,
    label
}) {


    return (
        <div>
            <Autocomplete
                id="area-search-box"
                options={autoCompleteList}
                getOptionLabel={(option) => option.title}
                style={{ width: "100%" }}
                renderInput={(params) => <TextField {...params} label={label} variant="outlined" />}
            />
        </div>
    );
}

export default Filters;
