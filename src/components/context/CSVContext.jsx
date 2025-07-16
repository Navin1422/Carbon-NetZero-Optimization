// src/context/CSVContext.jsx
import React, { createContext, useContext, useState } from 'react';



export const CSVContext = createContext({
  csvData: [],
  setCsvData: () => {},
});


export const CSVProvider = ({ children }) => {
  const [csvData, setCsvData] = useState([]);

  return (
    <CSVContext.Provider value={{ csvData, setCsvData }}>
      {children}
    </CSVContext.Provider>
  );
};

export const useCSV = () => useContext(CSVContext);
