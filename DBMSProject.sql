--
-- Database: `genetic_disorder_db`
--
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- --------------------------------------------------------
--
-- Table structure for `Clinic`
--
CREATE TABLE `Clinic` (
  `ClinicID` INT NOT NULL AUTO_INCREMENT,
  `ClinicName` VARCHAR(255) NOT NULL,
  `Address` TEXT,
  PRIMARY KEY (`ClinicID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Doctor`
--
CREATE TABLE `Doctor` (
  `DoctorID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(100) NOT NULL,
  `Specialization` VARCHAR(255),
  `ClinicID` INT,
  PRIMARY KEY (`DoctorID`),
  FOREIGN KEY (`ClinicID`) REFERENCES `Clinic`(`ClinicID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Patient`
--
CREATE TABLE `Patient` (
  `PatientID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(100) NOT NULL,
  `DateOfBirth` DATE,
  `Gender` VARCHAR(50),
  `ContactNo` VARCHAR(20),
  `Address` TEXT,
  PRIMARY KEY (`PatientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Appointment`
--
CREATE TABLE `Appointment` (
  `AppointmentID` INT NOT NULL AUTO_INCREMENT,
  `AppointmentDate` DATE,
  `AppointmentTime` TIME,
  `PatientID` INT,
  `DoctorID` INT,
  PRIMARY KEY (`AppointmentID`),
  FOREIGN KEY (`PatientID`) REFERENCES `Patient`(`PatientID`) ON DELETE CASCADE,
  FOREIGN KEY (`DoctorID`) REFERENCES `Doctor`(`DoctorID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `GeneticDisorder`
--
CREATE TABLE `GeneticDisorder` (
  `DisorderID` INT NOT NULL AUTO_INCREMENT,
  `DisorderName` VARCHAR(255) NOT NULL,
  `GeneSymbol` VARCHAR(50),
  `OMIM_ID` VARCHAR(50),
  PRIMARY KEY (`DisorderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `FamilyHistory`
-- Connects a patient (PatientID_FK) to a family member (FamilyMemberID_FK),
-- who is also a patient in the Patient table.
--
CREATE TABLE `FamilyHistory` (
  `PatientID_FK` INT NOT NULL,
  `FamilyMemberID_FK` INT NOT NULL,
  `Relationship` VARCHAR(100),
  PRIMARY KEY (`PatientID_FK`, `FamilyMemberID_FK`),
  FOREIGN KEY (`PatientID_FK`) REFERENCES `Patient`(`PatientID`) ON DELETE CASCADE,
  FOREIGN KEY (`FamilyMemberID_FK`) REFERENCES `Patient`(`PatientID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `DiagnosedWith`
-- Junction table for the M:N relationship between Patient and GeneticDisorder.
--
CREATE TABLE `DiagnosedWith` (
    `PatientID_FK` INT NOT NULL,
    `DisorderID_FK` INT NOT NULL,
    `AffectedStatus` VARCHAR(50),
    PRIMARY KEY (`PatientID_FK`, `DisorderID_FK`),
    FOREIGN KEY (`PatientID_FK`) REFERENCES `Patient`(`PatientID`),
    FOREIGN KEY (`DisorderID_FK`) REFERENCES `GeneticDisorder`(`DisorderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `FamilyDisorder`
-- Links a family history record to a specific disorder.
--
CREATE TABLE `FamilyDisorder` (
    `PatientID_FK` INT NOT NULL,
    `FamilyMemberID_FK` INT NOT NULL,
    `DisorderID_FK` INT NOT NULL,
    PRIMARY KEY (`PatientID_FK`, `FamilyMemberID_FK`, `DisorderID_FK`),
    FOREIGN KEY (`PatientID_FK`, `FamilyMemberID_FK`) REFERENCES `FamilyHistory`(`PatientID_FK`, `FamilyMemberID_FK`),
    FOREIGN KEY (`DisorderID_FK`) REFERENCES `GeneticDisorder`(`DisorderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `GeneVariant`
--
CREATE TABLE `GeneVariant` (
  `VariantID` INT NOT NULL AUTO_INCREMENT,
  `GeneSymbol` VARCHAR(50),
  `VariantName` VARCHAR(255),
  `Classification` VARCHAR(100),
  PRIMARY KEY (`VariantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Genetic_Test`
--
CREATE TABLE `Genetic_Test` (
  `TestID` INT NOT NULL AUTO_INCREMENT,
  `TestType` VARCHAR(255),
  `Methodology` TEXT,
  PRIMARY KEY (`TestID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Test`
--
CREATE TABLE `Test` (
  `ResultID` INT NOT NULL AUTO_INCREMENT,
  `TestDate` DATE,
  `PatientID` INT,
  `VariantID` INT,
  `GeneticTestID` INT,
  PRIMARY KEY (`ResultID`),
  FOREIGN KEY (`PatientID`) REFERENCES `Patient`(`PatientID`) ON DELETE CASCADE,
  FOREIGN KEY (`VariantID`) REFERENCES `GeneVariant`(`VariantID`) ON DELETE SET NULL,
  FOREIGN KEY (`GeneticTestID`) REFERENCES `Genetic_Test`(`TestID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- Table structure for `Patient_Audit_Log`
--
CREATE TABLE `Patient_Audit_Log` (
    `LogID` INT PRIMARY KEY AUTO_INCREMENT,
    `PatientID` INT,
    `ChangedField` VARCHAR(100),
    `OldValue` VARCHAR(255),
    `NewValue` VARCHAR(255),
    `ChangedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `ChangedBy` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
--
-- POPULATING DATA
--
-- --------------------------------------------------------

INSERT INTO `Clinic` (ClinicID, ClinicName, Address) VALUES
(101, 'Genomic Health Center', '123 Gene Way, Biotech City'),
(102, 'The Variant Institute', '45 Park Ave, Research Town'),
(103, 'Pediatric Genetics Clinic', '789 Kid St, Northwood'),
(104, 'Regional DNA Diagnostics', '10 Lab Rd, Southfield'),
(105, 'Inherited Disease Center', '20 Medical Pl, Westburg');

INSERT INTO `Doctor` (DoctorID, FirstName, LastName, Specialization, ClinicID) VALUES
(201, 'Alice', 'Smith', 'Clinical Geneticist', 101),
(202, 'Robert', 'Jones', 'Molecular Pathologist', 102),
(203, 'Elena', 'Garcia', 'Pediatric Geneticist', 103),
(204, 'David', 'Lee', 'Genetic Counselor', 104),
(205, 'Maria', 'Chen', 'Oncogenetics', 105),
(206, 'Omar', 'Hassan', 'Cytogeneticist', 101);

INSERT INTO `Patient` (PatientID, FirstName, LastName, DateOfBirth, Address, ContactNo, Gender) VALUES
(301, 'Ethan', 'Miller', '1995-05-15', '1 Oak St', '555-1001', 'M'),
(302, 'Olivia', 'Davis', '1988-11-20', '2 Birch Ave', '555-1002', 'F'),
(303, 'Liam', 'Wilson', '2010-03-01', '3 Pine Ln', '555-1003', 'M'),
(304, 'Sophia', 'Brown', '1975-08-25', '4 Maple Cir', '555-1004', 'F'),
(305, 'Noah', 'Taylor', '2005-01-10', '5 Elm Dr', '555-1005', 'M'),
(306, 'Emma', 'Moore', '1962-07-30', '6 Willow Rd', '555-1006', 'F');

INSERT INTO `Appointment` (AppointmentID, AppointmentDate, AppointmentTime, PatientID, DoctorID) VALUES
(401, '2025-10-20', '10:00:00', 301, 201),
(402, '2025-10-20', '14:30:00', 302, 202),
(403, '2025-10-21', '09:00:00', 303, 203),
(404, '2025-10-21', '11:00:00', 304, 205),
(405, '2025-11-05', '13:00:00', 305, 204),
(406, '2025-11-05', '15:00:00', 306, 201);

INSERT INTO `FamilyHistory` (PatientID_FK, FamilyMemberID_FK, Relationship) VALUES
(301, 306, 'Mother'),
(306, 301, 'Son'),
(304, 302, 'Sister'),
(302, 304, 'Sister'),
(303, 306, 'Aunt'),
(305, 303, 'Brother');

INSERT INTO `GeneticDisorder` (DisorderID, DisorderName, GeneSymbol, OMIM_ID) VALUES
(601, 'Cystic Fibrosis', 'CFTR', '219700'),
(602, 'Huntingtons Disease', 'HTT', '143100'),
(603, 'BRCA1-related Breast Cancer', 'BRCA1', '113705'),
(604, 'Sickle Cell Anemia', 'HBB', '603903'),
(605, 'Fragile X Syndrome', 'FMR1', '300624'),
(606, 'Duchenne Muscular Dystrophy', 'DMD', '310200');

INSERT INTO `DiagnosedWith` (PatientID_FK, DisorderID_FK, AffectedStatus) VALUES
(301, 601, 'Carrier'),
(302, 603, 'Affected'),
(303, 604, 'Affected'),
(304, 603, 'Carrier'),
(305, 605, 'Affected'),
(306, 602, 'Affected');

INSERT INTO `FamilyDisorder` (PatientID_FK, FamilyMemberID_FK, DisorderID_FK) VALUES
(301, 306, 602), -- Ethan's mother (306) has Huntington's
(306, 301, 601), -- Emma's son (301) is a CF carrier
(304, 302, 603), -- Sophia's sister (302) has BRCA1 cancer
(302, 304, 603), -- Olivia's sister (304) is a BRCA1 carrier
(305, 303, 604), -- Noah's brother (303) has Sickle Cell Anemia
(306, 303, 604); -- Emma's nephew (303) has Sickle Cell Anemia

INSERT INTO `GeneVariant` (VariantID, GeneSymbol, VariantName, Classification) VALUES
(901, 'CFTR', 'p.F508del', 'Pathogenic'),
(902, 'BRCA1', 'c.181T>G', 'Pathogenic'),
(903, 'HTT', 'Expansion', 'Pathogenic'),
(904, 'HBB', 'p.Glu6Val', 'Pathogenic'),
(905, 'CFTR', 'p.G551D', 'Pathogenic'),
(906, 'BRCA1', 'c.5222G>A', 'VUS');

INSERT INTO `Genetic_Test` (TestID, TestType, Methodology) VALUES
(1001, 'Cystic Fibrosis Panel', 'NGS'),
(1002, 'Oncogenetics Panel', 'NGS'),
(1003, 'Huntington Repeat Assay', 'PCR'),
(1004, 'Single Gene Sequencing', 'Sanger'),
(1005, 'Sickle Cell Screen', 'Electrophoresis'),
(1006, 'Whole Exome Sequencing', 'NGS');

INSERT INTO `Test` (ResultID, TestDate, PatientID, GeneticTestID, VariantID) VALUES
(1101, '2025-09-01', 301, 1001, 901), -- Ethan's CF test found F508del
(1102, '2025-09-10', 302, 1002, 902), -- Olivia's Oncogenetics test found BRCA1 c.181T>G
(1103, '2025-09-15', 303, 1005, 904), -- Liam's Sickle Cell test found p.Glu6Val
(1104, '2025-09-20', 304, 1002, 906), -- Sophia's Oncogenetics test found BRCA1 c.5222G>A
(1105, '2025-09-25', 305, 1006, 905), -- Noah's WES test found CFTR G551D
(1106, '2025-10-01', 306, 1003, 903); -- Emma's Huntington test found HTT Expansion

-- --------------------------------------------------------
--
-- PROCEDURES, FUNCTIONS, AND TRIGGERS
--
-- --------------------------------------------------------

--
-- Procedure: `sp_GetPatientFullReport`
--
DELIMITER //
CREATE PROCEDURE `sp_GetPatientFullReport` (
    IN `in_PatientID` INT
)
BEGIN
    
    -- 1. Get Patient's Personal Details
    SELECT 
        PatientID, 
        FirstName, 
        LastName, 
        DateOfBirth, 
        Address, 
        ContactNo, 
        Gender
    FROM 
        Patient
    WHERE 
        PatientID = in_PatientID;
        
    -- 2. Get Patient's Diagnosed Disorders
    SELECT 
        gd.DisorderName, 
        gd.GeneSymbol, 
        dw.AffectedStatus
    FROM 
        DiagnosedWith AS dw
    JOIN 
        GeneticDisorder AS gd ON dw.DisorderID_FK = gd.DisorderID
    WHERE 
        dw.PatientID_FK = in_PatientID;
        
    -- 3. Get Patient's Family History of Disorders
    SELECT 
        p_member.FirstName AS FamilyMemberFirstName,
        p_member.LastName AS FamilyMemberLastName,
        fh.Relationship,
        gd.DisorderName AS FamilyMemberDisorder
    FROM 
        FamilyHistory AS fh
    JOIN 
        Patient AS p_member ON fh.FamilyMemberID_FK = p_member.PatientID
    JOIN 
        FamilyDisorder AS fd ON fh.PatientID_FK = fd.PatientID_FK AND fh.FamilyMemberID_FK = fd.FamilyMemberID_FK
    JOIN 
        GeneticDisorder AS gd ON fd.DisorderID_FK = gd.DisorderID
    WHERE 
        fh.PatientID_FK = in_PatientID;
        
END//
DELIMITER ;

-- --------------------------------------------------------
--
-- Function: `fn_GetPatientAge`
--
DELIMITER //
CREATE FUNCTION `fn_GetPatientAge` (
    `in_PatientID` INT
)
RETURNS INT
DETERMINISTIC
BEGIN
    
    DECLARE dob DATE;
    DECLARE age INT;
    
    -- Find the patient's date of birth
    SELECT DateOfBirth INTO dob
    FROM Patient
    WHERE PatientID = in_PatientID;
    
    -- Calculate the age
    SET age = TIMESTAMPDIFF(YEAR, dob, CURDATE());
    
    -- Return the single value
    RETURN age;
    
END//
DELIMITER ;

-- --------------------------------------------------------
--
-- Trigger: `trg_PatientAudit`
--
DELIMITER //
CREATE TRIGGER `trg_PatientAudit`
AFTER UPDATE ON `Patient`
FOR EACH ROW
BEGIN
    
    -- Check if the ContactNo was the field that changed
    IF OLD.ContactNo <> NEW.ContactNo THEN
        
        -- Insert a record of the change into the audit log
        INSERT INTO Patient_Audit_Log 
            (PatientID, ChangedField, OldValue, NewValue, ChangedBy)
        VALUES 
            (OLD.PatientID, 'ContactNo', OLD.ContactNo, NEW.ContactNo, USER());
            
    END IF;
    
END//
DELIMITER ;

-- --------------------------------------------------------

--
-- Finalize the transaction.
--
COMMIT;