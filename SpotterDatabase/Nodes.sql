CREATE TABLE [dbo].[Nodes]
(
	[Id] INT NOT NULL PRIMARY KEY IDENTITY(1,1), 
    [Address] NVARCHAR(50) NOT NULL, 
    [Latitude] FLOAT NOT NULL, 
    [Longitude] FLOAT NOT NULL, 
    [IsLive] BIT NOT NULL, 
    [LastCheckin] DATETIME NULL
)
