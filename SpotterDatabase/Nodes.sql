CREATE TABLE [dbo].[Nodes]
(
	[Id] INT NOT NULL PRIMARY KEY IDENTITY(1,1), 
	[Name] NVARCHAR(50) NOT NULL,
    [Address] NVARCHAR(50) NOT NULL, 
    [Latitude] FLOAT NOT NULL, 
    [Longitude] FLOAT NOT NULL,
    [LastCheckin] DATETIME NULL    
)
