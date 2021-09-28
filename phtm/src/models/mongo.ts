
class Mongo {
    model: any = {
        answer: {
            category: String, // todo
            salesTarget: Number,
            budget: Number,
            meetingPlaces: Number,
            visitTime: Number,
            productKnowledgeTraining: Number,
            vocationalDevelopment: Number,
            regionTraining: Number,
            performanceTraining: Number,
            salesAbilityTraining: Number,
            assistAccessTime: Number,
            abilityCoach: Number,
            strategAnalysisTime: Number,
            adminWorkTime: Number,
            clientManagementTime: Number,
            kpiAnalysisTime: Number,
            teamMeetingTime: Number,
            resource: { link: "resource", inverse: "answerResource" },
            product: { link: "product", inverse: "answerProduct" },
            target: { link: "hospital", inverse: "answerHospital" },
        },
        evaluation: {
            proposalEvaluation: { link: "proposal", inverse: "evaluations" },
            category: String, // todo
            level: String,
            abilityDescription: String,
            awardDescription: String,
            levelDescription: String,
            actionDescription: String
        },
        final: {
            projectFinals: { link: "project", inverse: "finals" },
            sales: Number,
            quota: Number,
            budget: Number,
            quotaAchv: Number,
            salesForceProductivity: Number,
            roi: Number,
            newAccount: Number,
            generalPerformance: Number,
            resourceAssigns: Number,
            regionDivision: Number,
            targetAssigns: Number,
            manageTime: Number,
            manageTeam: Number
        },
        hospital: {
            answerHospital: { link: "answer", inverse: "target" },
            avatar: { link: "image", inverse: "hospitalAvatar" },
            presetHospital: { link: "preset", inverse: "hospital" },
            proposalTargets: { link: "proposal", inverse: "targets" },
            reportHospital: { link: "report", inverse: "hospital" },
            name: String,
            describe: String,
            regtime: String,
            position: String,
            code: String,
            avatarPath: String,
            category: String,
            level: String,
            docterNumber: Number,
            bedNumber: Number,
            income: Number,
            spaceBelongs: String,
            abilityToPay: String,
            selfPayPercentage: Number,
            patientNum: Number,
            patientNumA: Number,
            patientNumB: Number,
            policies: {link: "policy", isArray: true, inverse: "hospitalPolicies"},
            region: {link: "region", inverse: "hospitalRegion"},
        },
        image: {
            hospitalAvatar: { link: "hospital", inverse: "avatar" },
            levelRankImg: {link: "level", inverse: "rankImg"},
            levelAwardImg: {link: "level", inverse: "awardImg"},
            periodAnswers: {link: "period", inverse: "answers"},
            productAvatar: {link: "product", inverse: "avatar"},
            resourceAvatar: {link: "resource", inverse: "avatar"},
            img: String,
            tag: String,
            flag: Number,
        },
        level: {
            rank: String,
            rankImg: {link: "image", inverse: "levelRankImg"},
            awardImg: {link: "image", inverse: "levelAwardImg"},
        },
        period: {
            projectPeriods: {link: "project", inverse: "periods"},
            phase: Number,
            name: String,
            answers: {link: "image", isArray: true, inverse: "periodAnswers"},
            reports: {link: "report", isArray: true, inverse: "periodReports"},
        },
        policy: {
            hospitalPolicies: {link: "hospital", inverse: "policies"},
            name: String,
            describe: String,
        },
        preset: {
            proposal: {link: "proposal", inverse: "presetProposal"},
            proposalId: String,
            projectId: String,
            periodId: String,
            product: {link: "product", inverse: "presetProduct"},
            hospital: {link: "hospital", inverse: "presetHospital"},
            resource: {link: "resource", inverse: "presetResource"},
            phase: Number,
            category: Number,
            lastQuota: Number,
            lastSales: Number,
            lastAchievement: Number,
            potential: Number,
            lastShare: Number,
            currentTMA: Number,
            currentSalesSkills: Number,
            currentProductKnowledge: Number,
            currentBehaviorEfficiency: Number,
            currentWorkMotivation: Number,
            currentTargetDoctorNum: Number,
            currentTargetDoctorCoverage: Number,
            currentClsADoctorVT: Number,
            currentClsBDoctorVT: Number,
            currentClsCDoctorVT: Number,
            currentPatientNum: Number,
            currentDurgEntrance: String,
            currentPolicy: String,
            lastBudget: Number,
            initBudget: Number,
        },
        product: {
            answerProduct: {link: "answer", inverse: "product"},
            presetProduct: {link: "preset", inverse: "product"},
            proposalProducts: {link: "proposal", inverse: "products"},
            reportProduct: {link: "report", inverse: "product"},
            name: String,
            productCategory: String,
            medicateCategory: String,
            producer: String,
            avatar: {link: "image", inverse: "productAvatar"},
            avatarPath: String,
            safety: String,
            effectiveness: String,
            convenience: String,
            productType: Number,
            priceType: String,
            price: Number,
            cost: Number,
            launchDate: String,
            treatmentArea: String,
            feature: String,
            targetDepartment: String,
            patentDescribe: String,
            costEffective: String,
            lifeCycle: String,
        },
        project: {
            accountId: String,
            proposal: {link: "proposal", inverse: "projectProposal"},
            current: Number,
            pharse: Number,
            status: Number,
            startTime: Number,
            endTime: Number,
            lastUpdate: Number,
            periods: {link: "period", isArray: true, inverse: "projectPeriods"},
            finals: {link: "final", isArray: true, inverse: "projectFinals"},
        },
        proposal: {
            presetProposal: {link: "preset", inverse: "proposal"},
            projectProposal: {link: "project", inverse: "proposal"},
            usableProposalProposal: {link: "usableProposal", inverse: "proposal"},
            name: String,
            describe: String,
            totalPhase: Number,
            case: String,
            periodStep: String,
            periodBase: Number,
            products: {link: "product", isArray: true, inverse: "proposalProducts"},
            targets: {link: "hospital", isArray: true, inverse: "proposalTargets"},
            resources: {link: "resource", isArray: true, inverse: "proposalResources"},
            evaluations: {link: "evaluation", isArray: true, inverse: "proposalEvaluation"},
            quota: {link: "requirement", inverse: "proposalQuota"},
            validations: {link: "validation", isArray: true, inverse: "proposalValidations"}
        },
        region: {
            hospitalRegion: {link: "hospital", inverse: "region"},
            name: String,
            level: String,
            strategyPosition: String,
            localPatient: Number,
            outsidePatient: Number,
            patientNum: Number,
        },
        report: {
            periodReports: {link: "period", inverse: "reports"},
            category: String, // todo
            proposalId: String,
            projectId: String,
            periodId: String,
            hospital: {link: "hospital", inverse: "reportHospital"},
            product: {link: "product", inverse: "reportProduct"},
            resource: {link: "resource", inverse: "reportResource"},
            phase: Number,
            region: String,
            potential: Number,
            patientNum: Number,
            drugEntrance: String,
            sales: Number,
            salesContri: Number,
            salesQuota: Number,
            quotaGrowthMOM: Number,
            quotaContri: Number,
            required: Number,
            salesGrowthYOY: Number,
            salesGrowthMOM: Number,
            achievements: Number,
            ytd: Number,
        },
        requirement: {
            proposalQuota: {link: "proposal", inverse: "quota"},
            totalQuotas: Number,
            meetingPlaces: Number,
            visitingHours: Number,
            teamExperience: String,
            teamDescription: String,
            managerKpi: Number,
            mangementHours: Number,
            totalBudget: Number
        },
        resource: {
            answerResource: {link: "answer", inverse: "resource"},
            presetResource: {link: "preset", inverse: "resource"},
            proposalResources: {link: "proposal", inverse: "resources"},
            reportResource: {link: "report", inverse: "resource"},
            name: String,
            gender: Number,
            age: Number,
            education: String,
            professional: String,
            advantage: String,
            evaluation: String,
            experience: Number,
            totalTime: Number,
            entryTime: Number,
            avatar: {link: "image", inverse: "resourceAvatar"},
            avatarPath: String,
        },
        usableProposal: {
            accountId: String,
            proposal: {link: "proposal", inverse: "usableProposalProposal"},
        },
        validation: {
            proposalValidations: {link: "proposal", inverse: "validations"},
            validationType: String,
            expression: String,
            condition: String,
            error: String,
            leftValue: String,
            rightValue: String,
        }
    }

}

export default Mongo
