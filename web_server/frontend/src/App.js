import "./App.css";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { DataGrid } from "@mui/x-data-grid";
import { Button, TextField, Container, Box } from "@mui/material";
import { useEffect, useState } from "react";

const columns = [
    { field: "ticker", headerName: "Ticker", width: 333 },
    { field: "timestamp", headerName: "Date", width: 333 },
    { field: "price", headerName: "Price", width: 333 },
];

function App() {
    const [rows, setRows] = useState([]);
    const [searchValue, setSearchValue] = useState("");
    useEffect(() => {
        fetch("http://localhost:5000/items")
            .then((response) => response.json())
            .then((data) => {
                const mappedData = data.map((row) => {
                    return { ...row, id: row._id };
                });
                setRows(mappedData);
            });
        document.title = "Data Oracle";
    }, []);

    const searchByTicker = (requestedTicker) => {
        fetch(`http://localhost:5000/stock?ticker=${requestedTicker}`)
            .then((response) => response.json())
            .then((data) => {
                const mappedData = data.map((row) => {
                    return { ...row, id: row._id };
                });
                setRows(mappedData);
            });
    };

    return (
        <div className="App">
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static" style={{ backgroundColor: "#282c34", padding: 10 }}>
                    <Toolbar>
                        <Typography variant="h3">Stock Data Oracle</Typography>
                    </Toolbar>
                </AppBar>
            </Box>
            <div>
                <Container
                    component="form"
                    sx={{
                        "& .MuiTextField-root": { m: 1, width: "25ch" },
                    }}
                    noValidate
                    autoComplete="off"
                    flexDirection="row"
                >
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "row",
                            width: "100%",
                            justifyContent: "center",
                            alignItems: "center",
                            height: 200,
                        }}
                    >
                        <TextField
                            label="Ticker"
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                        />
                        <Button
                            variant="contained"
                            sx={{ height: 40 }}
                            onClick={() => {
                                searchByTicker(searchValue);
                            }}
                        >
                            Search
                        </Button>
                    </div>
                    <DataGrid
                        rows={rows}
                        columns={columns}
                        pageSize={5}
                        rowsPerPageOptions={[5]}
                        sx={{ height: 500 }}
                    />
                </Container>
            </div>
        </div>
    );
}

export default App;
